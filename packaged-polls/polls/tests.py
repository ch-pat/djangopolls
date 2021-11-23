import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


# Create your tests here.

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):    
        """ 
        Question.was_published_recently() returns True for questions from the future. 
        Write a test for this case.
        Run tests with python manage.py test polls
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_questions(self):
        """
        Returns False for questions older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_questions(self):
        """
        Returns True for questions published today
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question published 'days' days from now (negative goes into the past)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """
        Message for when no questions exist
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_questions(self):
        """
        Questions not from the future are shown on the index page.
        """
        question = create_question("Past question", -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_future_question(self):
        """
        Questions from the future should not appear in the index.
        """
        question = create_question("Future question", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        """
        When both future and past questions are present, only past questions are shown.
        """
        question = create_question("Past question.", -30)
        # Simply create, we will only check that the past question is the only result
        create_question("Future question", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])


    def two_past_questions(self):
        """
        Check that multiple questions are shown.
        """
        question1 = create_question("Question 1", -30)
        question2 = create_question("Question 2", -20)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question1, question2])


class QuesionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        If trying to see details of a question from the future, return 404.
        """
        question = create_question("Future question", 30)
        url = reverse('polls:detail', args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        Past questions' detail should be shown
        """
        question = create_question("Past question", -30)
        url = reverse('polls:detail', args=(question.id,))
        response = self.client.get(url)
        self.assertContains(response, question.question_text)

