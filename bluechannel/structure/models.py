from django.db import models

# Create your models here.
class Section(models.Model):
    name = models.CharField(blank=True, max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child')
    slug = models.SlugField(prepopulate_from=("name",))
    in_nav = models.BooleanField(default=True)
    order = models.IntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        if self.parent is null:
            return '/%s/' % self.slug
        
        section = self
        section_list = []
        
        while section.parent is not null:
            section=section.parent
            section_list.append(section.slug)
            
        return '/%s/' % ('/'.join(section_list))
        
    def get_all_children(self):
        return Section.objects.filter(parent=self.id)
        
    def get_all_siblings(self):
        return Section.objects.filter(parent=self.parent)
        
    class Admin:
        save_on_top = True
        search_fields = ['name', 'description',]
        list_display = ['name', 'parent', 'description']
        pass