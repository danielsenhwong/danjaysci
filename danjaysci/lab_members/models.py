from django.db import models
from datetime import date

# Create your models here.
class LabMember(models.Model):
    # Make a list of years that people could have joined the lab
    YEAR_LIST = list()
    for y in range(date.today().year - 40, date.today().year + 1):
        YEAR_LIST.append( (y, y) )
    # Convert the list to a tuple to be used in forms
    YEAR_TUPLE = tuple(YEAR_LIST)

    first_name = models.CharField(
        max_length = 30
    )

    last_name = models.CharField(
        max_length = 30
    )

    lab_job_title = models.ForeignKey(
        'LabPosition',
        help_text = "The current or last job title the named lab member had in this lab. This is used to track alumni, e.g. Brenda Eustace was a grad student in the lab."
    )

    start_year = models.PositiveIntegerField(
        choices = YEAR_TUPLE,
        default = date.today().year,
        blank = True,
        null = True,
    )

    end_year = models.PositiveIntegerField(
        choices = YEAR_TUPLE,
        blank = True,
        null = True,
    )

    current_position = models.TextField(
        blank = True,
        null = True,
        help_text = "Leave blank for current members of the lab. For lab alumni, please include current job title along with company/institution/organization information.",
    )

    date_added = models.DateField(
        auto_now_add = True,
        help_text = "The date this person was added to the database.",
    )

    last_updated = models.DateField(
        help_text = "The date this person's information was last updated.",
        blank = True,
        null = True,
    )

    email_address = models.EmailField(
        blank = True,
        null = True,
        unique = True,
        help_text = "Primary e-mail address for this lab member. For current Tufts affiliates, please enter their Tufts e-mail address here.",
    )

    email_address_alt = models.EmailField(
        blank = True,
        null = True,
        unique = True,
        help_text = "An alternate e-mail address for this lab member, in case the primary becomes deactivated."
    )

    def __str__(self):
        output = '%s %s, %s (%d' % (
            self.first_name,
            self.last_name,
            self.lab_job_title,
            self.start_year
        )

        if not self.end_year:
            output += "-present)"
        elif self.end_year == self.start_year:
            output += ')'
        else:
            output += '-%d)' % (self.end_year)
        
        return output

    def name_str(self):
        output = '%s%s%s' % (self.first_name, unichr(160), self.last_name)
        return output
        name_str.short_description = 'Name'

    def lab_years(self):
        output = '%d' % (self.start_year)
    
        if not self.end_year:
            output += '-present'
        elif self.end_year == self.start_year:
            output += ''
        else:
            output += '-%d' % (self.end_year)
        return output

class LabPosition(models.Model):
    name = models.CharField(
        max_length = 64,
    )
    
    abbreviation  = models.CharField(
        max_length = 24,
    )
    
    description = models.TextField(
        blank = True,
        null = True,
    )
  
    def __str__(self):
        output = "%s" % (self.name)
    
        return output
