from django.db import models 
from datetime import datetime, timedelta

class Post(models.Model):
    title = models.CharField(max_length = 100) # 제목 
    content = models.TextField(blank=True) # 내용
    created_at = models.DateTimeField(auto_now_add=True) # 작성날짜
    updated_at = models.DateTimeField(auto_now=True) # 수정날짜 
    end_at = models.DateTimeField(null=True) # 마감날짜
    priority = models.IntegerField(default=1) # 우선순위
    confirm = models.BooleanField(default=False)  

    def d_day(self): 
        if self.end_at == None:
            return "기한없음"
        else:
            time = self.end_at+timedelta(days=1) - datetime.now()
            if time.days == 0:
                return "d-day"
            elif time.days < 0:
                return "만료"
            elif time.days > 0:  
                return "d-"+str(time.days)

    def priority_range(self):
        
        return range(0,self.priority)

    class Meta:
        ordering = ['-updated_at'] 
    