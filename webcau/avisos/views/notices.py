from django.shortcuts import render
from django.views.generic import UpdateView, CreateView, DetailView, ListView
from django.views.generic.edit import FormMixin
from ..models import Member, Car, BaseNotice, ShortNotice
from ..forms import ShortNoticeForm, SendNoticeForm, ArrivedNoticeForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from dal import autocomplete
from datetime import datetime

###############################################################################
#                                  Mixins                                     #
###############################################################################

class NoticeAuthMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.member in self.get_object().allowed_to_edit()

###############################################################################
#                         Short Notice Autocompletes                          #
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

###############################################################################
#                              Short Notice CRUD                              #
###############################################################################

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

class UpdateShortNoticeView(NoticeAuthMixin, SuccessMessageMixin, UpdateView):
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

    def get_object(self):
        return Member.objects.get(user=self.request.user)

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

###############################################################################
#                            Short Notice Actions                             #
###############################################################################

class SendNoticeView(NoticeAuthMixin, SuccessMessageMixin, UpdateView):
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

class ArrivedNoticeView(NoticeAuthMixin, SuccessMessageMixin, UpdateView):
    model = ShortNotice
    form_class = ArrivedNoticeForm
    template_name = 'avisos/shortnotice/arrival.html'
    success_message = 'Aviso enviado correctamente.'

    def get_success_url(self):
         return reverse('avisos:detail_notice', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.arrival_confirmation_date = datetime.now()
        form.instance.arrival_confirmation_by = self.request.user.member
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ArrivedNoticeForm()
        context.update({'aviso': ShortNotice.objects.get(pk=self.kwargs['pk'])})
        context.update({'form': ArrivedNoticeForm(instance=self.object, initial={'arrival_confirmation_date': datetime.now(), 'arrival_confirmation_by': self.request.user.member})})
        return context
