from django import template
from django.utils.timesince import timesince
from posts.models import Post, Comment

register = template.Library()

@register.filter(name='shortened_timesince')
def shortened_timesince(value):
   time_diff = timesince(value) 
   time_diff = time_diff.replace('minutes', 'm').replace('minute', 'm')
   time_diff = time_diff.replace('hours', 'h').replace('hour', 'h')
   time_diff = time_diff.replace('days', 'd').replace('day', 'd')
   time_diff = time_diff.replace('months', 'mo').replace('month', 'mo')
   time_diff = time_diff.replace('years', 'y').replace('year', 'y')

   time_diff = time_diff.split(',')[0]

   return time_diff


@register.filter
def is_post(value):
   return isinstance(value, Post)

@register.filter
def is_comment(value):
   return isinstance(value, Comment)