from django.db import models

from register.models import Employee, WorkingPeriod

class Contract(models.Model):
    """
    Abstract representation of contracts. All contracts to be reported should
    extend this class.
    """
    employee = models.ForeignKey(Employee)
    workload = models.DecimalField(max_digits=4, decimal_places=2)

    def time_worked(self, start, end):
        """
        Returns how many hours the employee worked between the period.

        Let us suppose we have the following contract:

        >>> from register.tests.test_utilities import get_employee, clear_database
        >>> from register.models import WorkingPeriod
        >>> from datetime import datetime
        >>> clear_database()
        >>> employee = get_employee()
        >>> contract = Contract(employee=employee, workload=8)

        ...and its employee has the following working periods:
        
        >>> # Out the interval
        >>> wp = WorkingPeriod(employee=employee,
        ...         executed="test if employee has working period again",
        ...         start=datetime(2011, 3, 31, 14, 0, 0),
        ...         end=datetime(2011, 3, 31, 18, 0, 0))
        >>> wp.save()
        >>>     # in the interval
        >>> wp = WorkingPeriod(employee=employee,
        ...         executed="made the employe have it",
        ...        start=datetime(2011, 4, 5, 13, 0, 0),
        ...        end=datetime(2011, 4, 5, 18, 0, 0))
        >>> wp.save()
        >>> #out the interval
        >>> wp = WorkingPeriod(employee=employee,
        ...     executed="test if employee has working period again",
        ...     start=datetime(2011, 5, 1, 14, 0, 0),
        ...     end=datetime(2011, 5, 1, 18, 0, 0))
        >>> wp.save()

        If we invoke the method with a time interval which includes a period and
        excludes others:

        >>> start=datetime(2011, 4, 1)
        >>> end=datetime(2011, 4, 30)

        ...the result should be only the time of the periods included:

        >>> contract.time_worked(start, end)
        5.0

        >>> clear_database()
        """
        working_peridos = WorkingPeriod.objects.filter(
            start__gte=start, end__lte=end, employee=self.employee)

        time_worked = sum(period.total_time for period in working_peridos)

        return time_worked

    def due_payment(self, start, end):
        raise NotImplementedError("Contract.due_payment() not implemented. "
                "Your subclass of Contract should implement it.")

    class Meta:
        abstract=True
        db_tablespace='netunong_reports'

class PJContract(Contract):
    """
    Contract of "Pessoa Juridica" kind. The employee provides service to the
    employer through an individual, barebone company used only for burocratic
    necessity.
    """
    hour_value = models.DecimalField(max_digits=12, decimal_places=2)

    def due_payment(self, start, end):
        return self.time_worked(start, end)*self.hour_value

