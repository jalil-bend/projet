from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Conversation
from django.utils import timezone
from docteur.models import Doctor
from patient.models import Patient
from users.models import User
from django.contrib import messages
from django.db.models import Count
from datetime import datetime, timedelta
from django.utils.timezone import now
from users.models import Profile



User = get_user_model()

@login_required
def start_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if other_user == request.user:
        return redirect('messaging:inbox')

    my_speciality = request.user.profile.speciality
    other_speciality = other_user.profile.speciality

    if my_speciality in ['ophtalmologue', 'optometriste'] and other_speciality in ['ophtalmologue', 'optometriste']:
        context_type = 'doctor_doctor'
    else:
        context_type = 'doctor_patient'

    conversation = (
        Conversation.objects
        .annotate(num_participants=Count('participants'))
        .filter(participants=request.user, context_type=context_type, num_participants=2)
        .filter(participants=other_user)
        .first()
    )

    if not conversation:
        conversation = Conversation.objects.create(context_type=context_type)
        conversation.participants.add(request.user, other_user)

    return redirect('messaging:chat_view', conversation_id=conversation.id)



from .models import Conversation, Message
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required
def chat_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)

    try:
        doctor = Doctor.objects.get(profile=request.user.profile)
    except Doctor.DoesNotExist:
        doctor = None

    if request.method == 'POST':
        content = request.POST.get('content')
        file = request.FILES.get('file')


        if (content and content.strip()) or file:
            Message.objects.create(conversation=conversation, sender=request.user, content=content, file=file)
            conversation.last_updated = timezone.now()
            conversation.save()
        return redirect('messaging:chat_view', conversation_id=conversation.id)

    messages = conversation.messages.all()

    # ✅ Marquer les messages comme lus
    unread_messages = conversation.messages.filter(is_read=False).exclude(sender=request.user)
    unread_messages.update(is_read=True)

    receiver = conversation.participants.exclude(id=request.user.id).first()
    is_receiver_typing = hasattr(receiver, 'profile') and receiver.profile.is_typing
    is_online = False
    if hasattr(receiver, 'profile'):
        last_seen = receiver.profile.last_seen
        if last_seen:
            is_online = now() - last_seen < timedelta(seconds=60)

    return render(request, 'messaging/chat.html', {
        'conversation': conversation,
        'messages': messages,
        'receiver': receiver,
        'is_online': is_online,
        'is_receiver_typing': is_receiver_typing,
        'doctor': doctor,
    })


def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    if request.user in conversation.participants.all():
        conversation.deleted_by.add(request.user)  # Soft delete individuel
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'unauthorized'}, status=403)

import json
from django.http import JsonResponse
from .models import Conversation, Message
from django.core.serializers.json import DjangoJSONEncoder

def export_conversation_json(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    if request.user not in conversation.participants.all():
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    messages = conversation.messages.all().values(
        'sender__username', 'content', 'timestamp', 'is_read', 'is_edited'
    )

    return JsonResponse(
        list(messages),
        safe=False,
        json_dumps_params={'cls': DjangoJSONEncoder}
    )

@login_required
def inbox_view(request):
    all_convs = Conversation.objects.filter(participants=request.user).order_by('-last_updated')

    seen_users = set()
    inbox_data = []

    for conv in all_convs:
        other_user = conv.participants.exclude(id=request.user.id).first()
        if other_user and other_user.id not in seen_users:
            seen_users.add(other_user.id)

            profile = getattr(other_user, 'profile', None)
            if profile:
                last_seen = profile.last_seen
                is_online = profile.is_online
            else:
                last_seen = None
                is_online = False

            unread_count = conv.messages.filter(is_read=False).exclude(sender=request.user).count()

            inbox_data.append({
                'conversation': conv,
                'other_user': other_user,
                'unread_count': unread_count,
                'is_online': other_user.profile.is_online,
                'last_seen': other_user.profile.last_seen,
            })

    try:
        doctor = Doctor.objects.get(profile=request.user.profile)
    except Doctor.DoesNotExist:
        doctor = None

    return render(request, 'messaging/inbox.html', {
        'inbox_data': inbox_data,
        'doctor': doctor
    })

from django.http import JsonResponse

@login_required
def get_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    if request.user not in conversation.participants.all():
        return JsonResponse({'error': 'unauthorized'}, status=403)

    
    unread_messages = conversation.messages.filter(is_read=False).exclude(sender=request.user)
    unread_messages.update(is_read=True)

    msgs = conversation.messages.all()
    data = [{
        'sender_id': msg.sender.id,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime("%H:%M"),
        'is_read': msg.is_read
    } for msg in msgs]

    return JsonResponse({'messages': data})

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def set_typing_status(request, conversation_id):
    if request.method == "POST":
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        typing = request.POST.get("typing") == "true"
        request.user.profile.is_typing = typing
        request.user.profile.last_typing = timezone.now()
        request.user.profile.save()
        return JsonResponse({'status': 'ok'})


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def update_typing_status(request, conversation_id):
    if request.method == "POST":
        is_typing = request.POST.get("typing") == "true"
        request.user.profile.is_typing = is_typing
        request.user.profile.save()
        return JsonResponse({'status': 'ok'})


from django.http import JsonResponse
from .models import Conversation

@login_required
def get_unread_message_count(request):
    count = 0
    conversations = Conversation.objects.filter(participants=request.user)
    for conv in conversations:
        count += conv.messages.filter(is_read=False).exclude(sender=request.user).count()
    return JsonResponse({'unread_count': count})



# Create your views here.
