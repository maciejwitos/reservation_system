from django.shortcuts import render, redirect, reverse
from django.views import View
from app.models import *
from django.http import HttpResponse
import datetime
from django.db.models import Q

class MainPage(View):

    def get(self, request):
        rooms = Room.objects.all()
        today = datetime.date.today()
        reservations = Reservation.objects.filter(date=today).values('room_id')
        id_list = []
        for id in reservations:
            i = (id.get('room_id'))
            id_list.append(i)
        return render(request, 'main_page.html', {"rooms": rooms,
                                                  "id_list": id_list})


class AddRoom(View):

    def get(self, request):
        return render(request, 'room_new.html')

    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')
        if name and capacity and projector:
            room = Room.objects.create(name=name, capacity=capacity, projector=projector)
            room.save()
            return redirect(reverse('room_details', kwargs={"id": room.id}))
        else:
            return render(request, 'error_message.html')


class RoomDetails(View):

    def get(self, request, id):
        room = Room.objects.filter(id=id)
        return render(request, 'room_details.html', {"room": room})


class DeleteRoom(View):

    def get(self, request, id):
        room = Room.objects.filter(id=id)
        room.delete()
        return redirect('/')


class EditRoom(View):

    def get(self, request, id):
        room = Room.objects.filter(id=id)
        return render(request, 'edit_room.html', {"room": room})

    def post(self, request, id):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')
        if name and capacity and projector:
            room = Room.objects.get(id=id)
            room.name = name
            room.capacity = capacity
            room.projector = projector
            room.save()
            return redirect(reverse('room_details', kwargs={"id": room.id}))
        else:
            return render(request, 'error_message.html')


class MakeReservation(View):

    def get(self, request, id):
        room = Room.objects.filter(id=id)
        reservations = Reservation.objects.filter(room=id)
        return render(request, 'reservation_add.html', {'room': room,
                                                        'reservations': reservations})

    def post(self, request, id):
        date = request.POST.get('date')
        comment = request.POST.get('comment')
        room = Room.objects.get(id=id)
        # validation is another reservation for that room and date exist
        reserv = Reservation.objects.filter(date=date, room=id).exists()
        if reserv == False:
            # validation is picked date is in the future
            today = datetime.date.today().strftime("%Y-%m-%d")
            today_formated = datetime.datetime.strptime(today, "%Y-%m-%d")
            reservation_date = datetime.datetime.strptime(date, "%Y-%m-%d")
            print(reservation_date)
            print(date)
            if reservation_date < today_formated:
                return render(request, 'error_message.html')
            else:
            # validation is all date are picked
                if date and room:
                    new_reservation = Reservation.objects.create(
                        date=date,
                        comment=comment,
                        room=room
                    )
                    new_reservation.save()
                return redirect("/reservation/all/")
        else:
            return render(request, 'error_message.html')


class DeleteReservation(View):

    def get(self, request, id):
        reservation = Reservation.objects.filter(id=id)
        reservation.delete()
        return redirect('/reservation/all/')


class AllReservation(View):

    def get(self, request):
        today = datetime.date.today()
        reservations = Reservation.objects.filter(date__gte=today).order_by('date')
        return render(request, "reservation_all.html", {'reservations': reservations})


class TodayReservations(View):

    def get(self, request):
        today = datetime.date.today()
        reservations = Reservation.objects.filter(date=today)
        return render(request, 'today_status.html', {'reservations': reservations})


class OpenSearch(View):

    def post(self, request):
        return render(request, 'search.html')


class Search(View):

    def get(self, request):
        return render(request, 'search.html')


    def post(self, request):
        room_name = request.POST.get('room_name')
        room_capacity = request.POST.get('room_capacity')
        reservation_date = request.POST.get('reservation_date')
        projector_is_available = request.POST.get('projector_is_available')
        if room_capacity == "":
            room_capacity = 1
        if reservation_date == "":
            today = datetime.date.today()
            reservations = Reservation.objects.filter(date=today).values('room_id')
        else:
            reservation_date = datetime.datetime.strptime(reservation_date, "%Y-%m-%d")
            reservations = Reservation.objects.filter(date=reservation_date).values('room_id')
        id_list = []
        for id in reservations:
            i = (id.get('room_id'))
            id_list.append(i)

        if projector_is_available is None:
            rooms = Room.objects.filter(name__icontains=room_name,
                                        capacity__gte=room_capacity)
            return render(request, 'search_result.html', {'rooms': rooms,
                                                          'id_list': id_list})
        else:
            rooms = Room.objects.filter(name__icontains=room_name,
                                        capacity__gte=room_capacity,
                                        projector=projector_is_available)
            return render(request, 'search_result.html', {'rooms': rooms,
                                                          'id_list': id_list})

