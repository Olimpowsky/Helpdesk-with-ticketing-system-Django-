import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Ticket, Message
from .form import CreateTicketForm, UpdateTicketForm
from django.contrib.auth.decorators import login_required

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST, request.FILES)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.ticket_status = 'Pending'
            var.save()
            messages.info(request, 'Zgłoszenie zostało wysłane')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Wystąpił błąd, zgłoszenie nie zostało wysłane')
            return redirect('create-ticket')

    else:
        form = CreateTicketForm()
        context = {'form':form}
        return render(request, 'ticket/create_ticket.html', context)

@login_required
def update_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdateTicketForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Zgłoszenie zostało zaktualizowane')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Wystąpił błąd')

    else:
        form = UpdateTicketForm()
        context = {'form':form}
        return render(request, 'ticket/update_ticket.html', context)
@login_required
def ticket_details(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket_messages = ticket.message_set.all().order_by('-date_created')

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            ticket = ticket,
            message = request.POST.get('message')
        )
        return redirect('ticket-details', pk=pk)

    context = {'ticket':ticket, 'ticket_messages':ticket_messages}
    return render(request, 'ticket/ticket_details.html', context)
@login_required
def all_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-date_created')
    context = {'tickets':tickets}
    return render(request, 'ticket/all_tickets.html', context)

@login_required
def ticket_queue(request):
    tickets = Ticket.objects.filter(ticket_status='Pending')
    context = {'tickets':tickets}
    return render(request, 'ticket/ticket_queue.html', context)
@login_required
def accept_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.assigned_to = request.user
    ticket.ticket_status = 'Active'
    ticket.accepted_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Zgłoszenie zostało przyjęte')
    return redirect('workspace')
@login_required
def close_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.ticket_status = 'Completed'
    ticket.is_resolved = True
    ticket.accepted_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Zgłoszenie zostało rozwiązane')
    return redirect('ticket-queue')
@login_required
def workspace(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=False)
    context = {'tickets':tickets}
    return render(request, 'ticket/workspace.html', context)
@login_required
def all_closed_tickets(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=True).order_by('-date_created')
    context = {'tickets':tickets}
    return render(request, 'ticket/all_closed_tickets.html', context)