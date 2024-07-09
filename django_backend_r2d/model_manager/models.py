from django.db import models, IntegrityError

class ModelName(models.Model):
    """
    Table to store valid model names. 
    Used to normalize model_id in diagram models.
    id | name | code | provider
    1 | gpt-4o | 1 | openai
    2 | gpt-4-turbo | 2 | openai
    3 | gpt-3.5-turbo | 3 |  openai
    4 | text-embedding-3-large | 4 | openai
    5 | text-embedding-3-small | 5 | openai
    """
    name = models.CharField(max_length=50, unique=True)
    code = models.PositiveSmallIntegerField(unique=True)
    provider = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Model Name"
        verbose_name_plural = "Model Names"
        ordering = ['code']

    def save(self, *args, **kwargs):
        # Prevent changes to predefined statuses
        if self.pk:
            raise IntegrityError("Modification of predefined job statuses is not allowed.")
        super().save(*args, **kwargs)