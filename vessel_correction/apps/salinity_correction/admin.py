# coding: utf-8
from django.contrib import admin
import models
from django import forms
from models import CtdSalinityCorrection
from models import GliderSalinityCorrection
# Register your models here.
from scb_mng_models.models.instrumentation import Deployment, Cruise, Instrument, Sensor
from scb_mng_models.models.data import Dataset
from django.db.models import Q

class AuditModelAdmin(admin.ModelAdmin):
    readonly_fields = ('created_on', 'created_by', 'updated_on', 'updated_by')

    def save_model(self, request, obj, form, change):
        obj.save(user=request.user)

class CustomDeploymentChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.deployment_name)

class CustomSensorChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.sensor_name)

class CustomCtdCorrectionDeploymentChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.ctd_salinity_correction_deployment.deployment_name)

# Admin forms
class CtdDeploymentAdminForm(forms.ModelForm):
    ctd_salinity_correction_deployment = CustomDeploymentChoiceField(queryset=Deployment.objects.filter(deployment_instrument__instrument_instrument_type__instrument_type_name__iexact='ctd'))
    ctd_salinity_correction_sensor_01 = CustomSensorChoiceField(queryset=Sensor.objects.filter(sensor_sensor_type__sensor_type_id__iexact='8'), required=False)
    ctd_salinity_correction_sensor_02 = CustomSensorChoiceField(queryset=Sensor.objects.filter(sensor_sensor_type__sensor_type_id__iexact='8'), required=False)
    class Meta:
        model = CtdSalinityCorrection
        fields = '__all__'


class GliderDeploymentAdminForm(forms.ModelForm):
    glider_salinity_correction_deployment = CustomDeploymentChoiceField(queryset=Deployment.objects.filter(deployment_instrument__instrument_instrument_type__instrument_type_name__iexact='glider'))
    glider_salinity_correction_background_data = CustomCtdCorrectionDeploymentChoiceField(queryset=CtdSalinityCorrection.objects.all())
    glider_salinity_correction_sensor_01 = CustomSensorChoiceField(queryset=Sensor.objects.filter(Q(sensor_sensor_type__sensor_type_id__iexact='15') | Q(sensor_sensor_type__sensor_type_id__iexact='74')), required=False)
    class Meta:
        model = GliderSalinityCorrection
        fields = '__all__'

# Admin Models
class CtdSalinityCorrectionAdmin(AuditModelAdmin):
    search_fields = ['ctd_salinity_correction_deployment_id']
    list_display = ('get_deployment', 'ctd_salinity_correction_approved_results', 'get_deployment_instrument', 'get_deployment_cruise',
                    'ctd_salinity_correction_sensor_01_corr_coeff', 'ctd_salinity_correction_sensor_01_std_resid', 'get_deployment_sensor_01',
                    'ctd_salinity_correction_sensor_02_corr_coeff', 'ctd_salinity_correction_sensor_02_std_resid', 'get_deployment_sensor_02',
                    'ctd_salinity_correction_flag')
    form = CtdDeploymentAdminForm

    def get_deployment(self, obj):
        if obj.ctd_salinity_correction_deployment:
            return obj.ctd_salinity_correction_deployment.deployment_name
        else:
            return

    get_deployment.short_description = 'Deployment'
    get_deployment.admin_order_field = 'ctd_salinity_correction_deployment__deployment_name'

    def get_deployment_instrument(self, obj):
        if obj.ctd_salinity_correction_deployment.deployment_instrument:
            return obj.ctd_salinity_correction_deployment.deployment_instrument.instrument_name
        else:
            return

    get_deployment_instrument.short_description = 'Instrument'
    get_deployment_instrument.admin_order_field = 'ctd_salinity_correction_deployment__deployment_instrument__instrument_name'

    def get_deployment_cruise(self, obj):
        if obj.ctd_salinity_correction_deployment.deployment_cruise:
            return obj.ctd_salinity_correction_deployment.deployment_cruise.cruise_name
        else:
            return

    get_deployment_cruise.short_description = 'Cruise'
    get_deployment_cruise.admin_order_field = 'ctd_salinity_correction_deployment__deployment_cruise__cruise_name'


    def get_deployment_sensor_01(self, obj):
        if obj.ctd_salinity_correction_sensor_01:
            return obj.ctd_salinity_correction_sensor_01.sensor_serial
        else:
            return

    get_deployment_sensor_01.short_description = 'Sensor 01'
    get_deployment_sensor_01.admin_order_field = 'ctd_salinity_correction_sensor_01__sensor_serial'

    def get_deployment_sensor_02(self, obj):
        if obj.ctd_salinity_correction_sensor_02:
            return obj.ctd_salinity_correction_sensor_02.sensor_serial
        else:
            return

    get_deployment_sensor_02.short_description = 'Sensor 02'
    get_deployment_sensor_02.admin_order_field = 'ctd_salinity_correction_sensor_02__sensor_serial'

class GliderSalinityCorrectionAdmin(AuditModelAdmin):
    search_fields = ['glider_salinity_correction_deployment_id']
    list_display = ('glider_salinity_correction_approved_results', 'get_deployment', 'get_deployment_code', 'get_deployment_instrument', 'get_deployment_initial_date', 'get_glider_sensor_01', 'get_ctd_correction')
    form = GliderDeploymentAdminForm

    def get_deployment(self, obj):
        if obj.glider_salinity_correction_deployment:
            return obj.glider_salinity_correction_deployment.deployment_name
        else:
            return

    get_deployment.short_description = 'Deployment Name'
    get_deployment.admin_order_field = 'glider_salinity_correction_deployment__deployment_name'

    def get_deployment_code(self, obj):
        if obj.glider_salinity_correction_deployment:
            return obj.glider_salinity_correction_deployment.deployment_code
        else:
            return

    get_deployment_code.short_description = 'Deployment Code'
    get_deployment_code.admin_order_field = 'glider_salinity_correction_deployment__deployment_code'

    def get_deployment_initial_date(self, obj):
        if obj.glider_salinity_correction_deployment:
            return obj.glider_salinity_correction_deployment.deployment_initial_date
        else:
            return

    get_deployment_initial_date.short_description = 'Deployment Initial Date'
    get_deployment_initial_date.admin_order_field = 'glider_salinity_correction_deployment__deployment_initial_date'


    def get_deployment_instrument(self, obj):
        if obj.glider_salinity_correction_deployment.deployment_instrument:
            return obj.glider_salinity_correction_deployment.deployment_instrument.instrument_name
        else:
            return

    get_deployment_instrument.short_description = 'Instrument'
    get_deployment_instrument.admin_order_field = 'glider_salinity_correction_deployment__deployment_instrument__instrument_name'

    def get_ctd_correction(self, obj):
        if obj.glider_salinity_correction_background_data:
            return obj.glider_salinity_correction_background_data.ctd_salinity_correction_deployment.deployment_name
        else:
            return

    get_ctd_correction.short_description = 'CTD Correction Deployment'
    get_ctd_correction.admin_order_field = 'glider_salinity_correction_deployment__deployment_name'

    def get_glider_sensor_01(self, obj):
        if obj.glider_salinity_correction_sensor_01:
            return obj.glider_salinity_correction_sensor_01.sensor_serial
        else:
            return

    get_glider_sensor_01.short_description = 'Sensor 01'
    get_glider_sensor_01.admin_order_field = 'glider_salinity_correction_sensor_01__sensor_serial'

admin.site.register(CtdSalinityCorrection, CtdSalinityCorrectionAdmin)
admin.site.register(GliderSalinityCorrection, GliderSalinityCorrectionAdmin)
