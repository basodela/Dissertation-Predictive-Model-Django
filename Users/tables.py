import django_tables2 as tables
from .models import Programme
from django_tables2.export.export import TableExport

class ProgrammeTable(tables.Table):
    class Meta:
        model = Programme
        fields = ['date', 'exercise', 'sets', 'reps', 'weight', 'notes']
        attrs = {'class': 'paleblue', 'width': '100%'}



