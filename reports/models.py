from django.db import models

from register.models import Employee, WorkingPeriod

class Contract(models.Model):
    employee = models.ForeignKey(Employee)
    workload = models.DecimalField(max_digits=4, decimal_places=2)
    salary = models.DecimalField(max_digits=12, decimal_places=2)

    def time_worked(self, start, end):
        working_peridos = WorkingPeriod.objects.filter(
            start__gte=start, end__lte=end, employee=self.employee)

        time_worked = sum(period.total_time for period in working_peridos)

        return time_worked
