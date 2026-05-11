from django.contrib import admin
from .models import SharedData


class SharedDataAdmin(admin.ModelAdmin):
   # list_display = ()   # hide columns
    #actions = None 



      # 1. Hides the "12 shared datas" full count text
    show_full_result_count = False 
    
    # 2. Removes the "Action" dropdown and selection checkboxes
    actions = None 

    # 3. If you want to hide the table itself without a template, 
    # you can empty the list_display.
    list_display = [] 
    
    # 4. To hide the bottom count completely, we limit the results to 0
    def get_queryset(self, request):
        return super().get_queryset(request).none()
admin.site.register(SharedData, SharedDataAdmin)