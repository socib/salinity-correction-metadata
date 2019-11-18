# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from vessel_correction.apps.base.models import AuditBaseModel
from scb_mng_models.models.instrumentation import Deployment, Instrument, Sensor

# queryset = Deployment.objects.all()
# DEPLOYMENT_CHOICES = ()
# for i in range(0,len(queryset)):
#     deployment_i = (queryset[i].deployment_id, queryset[i].deployment_id)
#     DEPLOYMENT_CHOICES = DEPLOYMENT_CHOICES + (deployment_i,)

# queryset = instrumentation.Cruise.objects.all()
# CRUISE_CHOICES = ()
# for i in range(0,len(queryset)):
#     cruise_name_i = (queryset[i].cruise_name, queryset[i].cruise_name)
#     CRUISE_CHOICES = CRUISE_CHOICES + (cruise_name_i,)
#
# queryset = instrumentation.Deployment.objects.all()
# DEPLOYMENT_CHOICES = ()
# for i in range(0,len(queryset)):
#     deployment_name_i = (queryset[i].deployment_name, queryset[i].deployment_name)
#     DEPLOYMENT_CHOICES = DEPLOYMENT_CHOICES + (deployment_name_i,)
#
FLAG_CHOICES = (
    ('good','GOOD'),
    ('bad', 'BAD'),
)

class CtdSalinityCorrection(AuditBaseModel):
    ctd_salinity_correction_id = models.AutoField(primary_key=True)
    ctd_salinity_correction_deployment = models.ForeignKey(Deployment, null=True, blank=False)
    # ctd_salinity_correction_deployment_id = models.ForeignKey(Deployment, max_length=50, choices=DEPLOYMENT_CHOICES, null=False, blank=True)
    # ctd_salinity_correction_deployment_id = models.CharField(_('Deployment name'), max_length=50, choices=DEPLOYMENT_CHOICES, null=False, blank=True)
    # name = models.ForeignKey(instrumentation.Cruise, null=True)
    # name = models.CharField(_('cruise name'), max_length=100, null=True, blank=True)
    # ctd_correction_deployment = models.CharField(_('deployment name'), max_length=50, choices=DEPLOYMENT_CHOICES, default='scb-sbe9002')
    # initial_date = models.DateField(_('initial date'), null=True, blank=True)
    # end_date = models.DateField(_('end date'), null=True, blank=True)
    # cruise_length = models.IntegerField(_('cruise length'), blank=True)
    # ctd_name = models.CharField(_('CTD instrument name'),max_length=12, choices=INSTRUMENT_CHOICES, default='scb-sbe9002')
    # ctd_serial = models.TextField(_('CTD serial number'), blank=True)
    ctd_salinity_correction_date_last_service_sensor_01 = models.DateField(_('date last service prior to cruise sensor 01'), null=True, blank=True)
    ctd_salinity_correction_interval_service_cruise_sensor_01 = models.IntegerField(_('interval service to cruise sensor 01'), null=True, blank=True)
    ctd_salinity_correction_date_last_service_sensor_02 = models.DateField(_('date last service prior to cruise sensor 02'), null=True, blank=True)
    ctd_salinity_correction_interval_service_cruise_sensor_02 = models.IntegerField(_('interval service to cruise sensor 02'), null=True, blank=True)
    ctd_salinity_correction_sensor_01_corr_coeff = models.FloatField(_('sensor 01 correction coefficient'), null=False, blank=False)
    ctd_salinity_correction_sensor_01_mean_resid = models.FloatField(_('sensor 01 residual salinity differences mean'), null=False, blank=False)
    ctd_salinity_correction_sensor_01_std_resid = models.FloatField(_('sensor 01 residual salinity differences std'), null=False, blank=False)
    ctd_salinity_correction_sensor_01 = models.ForeignKey(Sensor, null=True, blank=True, related_name='ctd_salinity_correction_sensor_01')
    ctd_salinity_correction_sensor_02_corr_coeff = models.FloatField(_('sensor 02 correction coefficient'), null=True, blank=True)
    ctd_salinity_correction_sensor_02_mean_resid = models.FloatField(_('sensor 02 residual salinity differences mean'), null=True, blank=True)
    ctd_salinity_correction_sensor_02_std_resid = models.FloatField(_('sensor 02 residual salinity differences std'), null=True, blank=True)
    ctd_salinity_correction_sensor_02 = models.ForeignKey(Sensor, blank=True, null=True, related_name='ctd_salinity_correction_sensor_02')
    ctd_salinity_correction_flag = models.CharField(_('flag'), max_length=10, choices=FLAG_CHOICES, null=True, blank=True)
    ctd_salinity_correction_outliers_removed = models.CharField(_('outliers removed'), max_length=100, null=True, blank=True)
    ctd_salinity_correction_comments = models.TextField(_('comments'), null=True, blank=True)
    ctd_salinity_correction_approved_results =  models.BooleanField(default=False)

    class Meta:
        verbose_name = _('CTD Salinity Correction')
        verbose_name_plural = _('CTD Salinity Corrections')
        db_table = '"corrections"."ctd_salinity_correction"'


    # def __unicode__(self):
    #     return self.ctd_salinity_correction_deployment

class GliderSalinityCorrection(AuditBaseModel):
    glider_salinity_correction_id = models.AutoField(primary_key=True)
    glider_salinity_correction_deployment = models.ForeignKey(Deployment, null=True, blank=False)
    glider_salinity_correction_date_last_service = models.DateField(_('date last service prior to mission'), null=True, blank=True)
    glider_salinity_correction_interval_service_mission = models.IntegerField(_('interval service to mission'), null=True, blank=True)
    glider_salinity_correction_sensor_01 = models.ForeignKey(Sensor, null=True, blank=True)
    glider_salinity_correction_sensor_01_corr_coeff = models.FloatField(_('sensor 01 correction coefficient'), blank=False, null=False)
    glider_salinity_correction_residual_salinity_differences = models.CharField(_('residual salinity differences std background data'), max_length=200, blank=False, null=False)
    glider_salinity_correction_salinity_error_estimate = models.FloatField(_('salinity error estimate'), blank=False, null=False)
    glider_salinity_correction_background_data = models.ForeignKey(CtdSalinityCorrection, blank=False, null=False)
    glider_salinity_correction_theta_sal_range = models.CharField(_('theta-sal whitespace for correction potential temperature and practical salinity ranges'), max_length=200, blank=False, null=False)
    glider_salinity_correction_comments = models.TextField(_('comments'), null=True, blank=True)
    glider_salinity_correction_approved_results =  models.BooleanField(default=False)
    class Meta:
        verbose_name = _('Glider Salinity Correction')
        verbose_name_plural = _('Glider Salinity Corrections')
        db_table = '"corrections"."glider_salinity_correction"'
