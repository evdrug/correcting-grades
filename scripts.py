import random

from django.db.models import F

from datacenter.models import Schoolkid, Lesson, Commendation


def search_schoolkid(child_name):
    if not child_name:
        print('Не указано ФИО ученика')
        return None
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=child_name)
    except Schoolkid.DoesNotExist:
        print('Нет такого ученика')
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников, введите данные точнее')
    else:
        print('Найден:', schoolkid.full_name,
              f'{schoolkid.year_of_study}{schoolkid.group_letter}')
        return schoolkid
    return None


def fix_marks(schoolkid):
    marks = schoolkid.mark_set.filter(points__lte=3)
    for mark in marks:
        mark.points = random.randint(4, 5)
        mark.save()


def remove_chastisements(schoolkid):
    return schoolkid.chastisement_set.all().delete()


def create_commendation(child_name, subject):
    praise = ('Отлично!', 'Хорошо!', 'Великолепно!', 'Прекрасно!',
              'Сказано здорово – просто и ясно!', 'Очень хороший ответ!',
              'Талантливо!', 'Потрясающе!', 'Замечательно!', 'Так держать!',
              'Ты на верном пути!', 'Здорово!', 'Я тобой горжусь!',
              'С каждым разом у тебя получается всё лучше!',
              'Я вижу, как ты стараешься!', 'Ты растешь над собой!',
              'Теперь у тебя точно все получится!')
    child = search_schoolkid(child_name)

    if not isinstance(child, Schoolkid):
        return None

    last_subjects = Lesson.objects.filter(year_of_study=child.year_of_study,
                                          group_letter=child.group_letter,
                                          subject__title=subject).order_by(
        F('date').desc()).first()
    if not last_subjects:
        print("Не найден урок")
        return None
    if last_subjects.subject.commendation_set.filter(schoolkid=child).count():
        print("На этом уроке уже хвалили ;-)")
        return None
    Commendation.objects.create(text=random.choice(praise),
                                created=last_subjects.date,
                                schoolkid=child,
                                subject=last_subjects.subject,
                                teacher=last_subjects.teacher
                                )
