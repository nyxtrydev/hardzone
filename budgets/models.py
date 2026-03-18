from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    total_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class BudgetAllocation(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='allocations', null=True, blank=True)
    employee = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='my_allocations', null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        target = self.employee.username if self.employee else self.department.name
        return f"Budget for {target}: {self.amount}"

class CompanySettings(models.Model):
    total_company_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return "Company Settings"

    class Meta:
        verbose_name_plural = "Company Settings"
