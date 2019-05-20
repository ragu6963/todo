from django.db import models 
from datetime import datetime, timedelta

class Post(models.Model):
    title = models.CharField(max_length = 100) # 제목 
    content = models.TextField(blank=True) # 내용
    created_at = models.DateTimeField(auto_now_add=True) # 작성날짜
    updated_at = models.DateTimeField(auto_now=True) # 수정날짜 
    end_at = models.DateTimeField(null=True) # 마감날짜
    priority = models.IntegerField(default=1) # 우선순위
    confirm = models.BooleanField(default=False) # 메모 확인 / 비확인

    class Meta: 
        ordering = ['-updated_at'] #기본 정렬 순서 : 수정날짜 내림차순

    def d_day(self): # 현재 날짜와 마감날짜 간의 차이 return method
        if self.end_at == None: # 마감날짜 없을 시
            return "기한없음"
        else:
            time = self.end_at+timedelta(days=1) - datetime.now()
            if time.days == 0:
                return "d-day"
            elif time.days < 0:
                return "만료"
            elif time.days > 0:  
                return "d-"+str(time.days)

    def priority_range(self): # 우선순위 범위
        
        return range(0,self.priority)