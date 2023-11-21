import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Ticket
from .form import CreatTicketForm, UpdateTicketForm



def create_ticket(request):
    if request.method == 'POST':
        form = CreatTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.ticket.status = 'Pending'
            var.save()
            messages.info(request, 'Zgłoszenie zostało wysłane')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Wystąpił błąd, zgłoszenie nie zostało wysłane')
            return redirect('create-ticket')

    else:
        form = CreatTicketForm()
        context = {'form':form}
        return render(request, 'ticket/create_ticket.html', context)
    
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

def ticket_details(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    context = {'ticket':ticket}
    return render(request, 'ticket/ticket_details.html', context)

def all_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    context = {'tickets':tickets}
    return render(request, 'ticket/all_tickets.html', context)


def ticket_queue(request):
    tickets = Ticket.objects.filter(ticket_status='Pending')
    context = {'tickets':tickets}
    return render(request, 'ticket/ticket_queue.html', context)

def accept_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.assigned_to = request.user
    ticket.ticket_status = 'Active'
    ticket.accepted_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Zgłoszenie zostało przyjęte')
    return redirect('ticket-queue')

def close_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.ticket_status = 'Completed'
    ticket.is_resolved = True
    ticket.accepted_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Zgłoszenie zostało rozwiązane')
    return redirect('ticket-queue')

def workspace(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=False)
    context = {'tickets':tickets}
    return render(request, 'ticket/workspace.html', context)

def all_closed_tickets(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=True)
# Create your views here.
