from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView, ListView, FormView
from django.views.generic.edit import FormMixin, ModelFormMixin
from django.views.generic.detail import SingleObjectMixin
from .models import Member, MedicalRecord, Car, EmergencyContact, BaseNotice, ShortNotice
from .forms import MemberForm, MedicalForm, CarForm, EmergencyContactForm, ShortNoticeForm, SendNoticeForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from dal import autocomplete
from itertools import chain
from datetime import datetime


class IndexView(LoginRequiredMixin, View):
    
    def get(self, request):
        return render(request, 'index.html', {'member': self.get_object(), 'cars': self.get_cars(), 'emergencycontacts': self.get_emergencycontacts()})

    def get_object(self):
        return Member.objects.get(user=self.request.user)
    
    def get_cars(self):
        return Car.objects.filter(member=self.get_object())
    
    def get_emergencycontacts(self):
        return EmergencyContact.objects.filter(member=self.get_object())

###############################################################################
#                         Mixin para modals con ajax                          #
###############################################################################
class AjaxTemplateMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split('.html')
            split[-1] = '_inner'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)

###############################################################################
#                                    Member                                   #
###############################################################################

class UpdateAccountView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'account/settings.html'
    success_url = reverse_lazy('account_data')
    success_message = 'Datos actualizados correctamente'

    def get_object(self):
        return Member.objects.get(user=self.request.user)

###############################################################################
#                                   Medical                                   #
###############################################################################

class UpdateMedicalView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MedicalRecord
    form_class = MedicalForm
    template_name = 'medical/settings.html'
    success_url = reverse_lazy('medical_data')
    success_message = 'Datos actualizados correctamente'

    def get_object(self):
        return MedicalRecord.objects.get(member=self.request.user.member)

###############################################################################
#                                     Car                                     #
###############################################################################

class CarsView(LoginRequiredMixin, View):
    template_name = 'car/index.html'

    def get(self, request):
        return render(request, self.template_name, {'cars': Car.objects.filter(member=request.user.member)})

class UpdateCarView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car/edit.html'
    success_url = reverse_lazy('cars_data')
    success_message = 'Datos actualizados correctamente'

class CreateCarView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car/create.html'
    success_url = reverse_lazy('cars_data')
    success_message = 'Vehículo creado correctamente'

    def form_valid(self, form):
        form.instance.member = self.request.user.member
        return super().form_valid(form)

class DeleteCarView(LoginRequiredMixin, DeleteView):
    model = Car
    success_url = reverse_lazy('cars_data')

###############################################################################
#                            Emergency Contact                                #
###############################################################################

class EmergencyContactsView(LoginRequiredMixin, View):
    template_name = 'emergencycontact/index.html'

    def get(self, request):
        return render(request, self.template_name, {'emergencycontacts': EmergencyContact.objects.filter(member=request.user.member).order_by('-main_contact')})

class UpdateEmergencyContactView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = EmergencyContact
    form_class = EmergencyContactForm
    template_name = 'emergencycontact/edit.html'
    success_url = reverse_lazy('emergencycontacts_data')
    success_message = 'Datos actualizados correctamente'

class CreateEmergencyContactView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = EmergencyContact
    form_class = EmergencyContactForm
    template_name = 'emergencycontact/create.html'
    success_url = reverse_lazy('emergencycontacts_data')
    success_message = 'Contacto creado correctamente'

    def form_valid(self, form):
        form.instance.member = self.request.user.member
        return super().form_valid(form)

class DeleteEmergencyContactView(LoginRequiredMixin, DeleteView):
    model = EmergencyContact
    success_url = reverse_lazy('emergencycontacts_data')

###############################################################################
#                               Short Notice                                  #
###############################################################################

class MemberAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Member.objects.none()

        qs = Member.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class CarsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Car.objects.none()

        qs = Car.objects.all()

        members = self.forwarded.get('participants', None)
        if members:
            qs_temp = Car.objects.none()
            for member_str in members:
                member = Member.objects.get(pk=member_str)
                qs_temp = qs_temp | qs.filter(member=member)
            qs = qs_temp
        if self.q:
            qs = qs.filter(license_plate__istartswith=self.q)

        return qs

class CreateShortNoticeView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ShortNotice
    form_class = ShortNoticeForm
    template_name = 'avisos/shortnotice/create.html'
    success_message = 'Aviso creado correctamente. Recuerda que debes enviarlo para que se active.'
    pk = None

    def form_valid(self, form):
        form.instance.member = self.request.user.member
        item = form.save()
        self.pk = item.pk
        return super().form_valid(form)
    
    def get_success_url(self):
         return reverse('avisos:detail_notice', kwargs={'pk': self.object.pk})

class UpdateShortNoticeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ShortNotice
    form_class = ShortNoticeForm
    template_name = 'avisos/shortnotice/edit.html'
    success_message = 'Aviso actualizado correctamente.'

    def get_success_url(self):
         return reverse('avisos:detail_notice', kwargs={'pk': self.object.pk})

class NoticesView(LoginRequiredMixin, ListView):
    model = BaseNotice
    template_name = 'avisos/index.html'
    title = ''

    class Meta:
        abstract = True

class AllNoticesView(NoticesView):
    title = 'Todos los Avisos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': self.title, 'avisos': BaseNotice.objects.all()})
        return context

class MyNoticesView(NoticesView):
    title = 'Mis Avisos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': self.title, 'avisos': BaseNotice.objects.filter(participants=self.request.user.member)})
        return context

class DetailNoticeView(LoginRequiredMixin, FormMixin, DetailView):
    model = ShortNotice
    template_name = 'avisos/shortnotice/detail.html'
    
    def get(self, request, pk):
        return render(request, self.template_name, {'aviso': BaseNotice.objects.get(pk=pk)})

class SendNoticeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ShortNotice
    form_class = SendNoticeForm
    template_name = 'avisos/shortnotice/send.html'
    success_message = 'Aviso enviado correctamente.'

    def get_success_url(self):
         return reverse('avisos:detail_notice', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.sent_date = datetime.now()
        form.instance.sent_by = self.request.user.member
        form.instance.sendto_caucontacts = True
        form.instance.sendto_participants = True
        form.instance.sendto_emergencycontacts = True
        form.instance.sendto_board = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SendNoticeForm()
        context.update({'aviso': ShortNotice.objects.get(pk=self.kwargs['pk'])})
        context.update({'form': SendNoticeForm(instance=self.object, initial={'sent_date': datetime.now(), 'sent_by': self.request.user.member})})
        return context

    # model = ShortNotice
    # form_class = SendNoticeForm
    # template_name = 'avisos/shortnotice/send.html'
    # success_message = 'Aviso enviado correctamente.'

    # def post(self, request, pk):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     print("WENA")
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    # def get(self, request, pk):
    #     return render(request, self.template_name, {'aviso': ShortNotice.objects.get(pk=pk)})

    # def get_success_url(self):
    #      return reverse('avisos:detail_notice', kwargs={'pk': self.object.pk})

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = SendNoticeForm()
    #     context.update({'aviso': ShortNotice.objects.get(pk=self.kwargs['pk'])})
    #     context.update({'form': SendNoticeForm(instance=self.object, initial={'sent_date': datetime.now(), 'sent_by': self.request.user.member})})
    #     return context
