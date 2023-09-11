from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.database import async_session_maker
from app.lessons.models import lesson_question_association
from app.quizes.models import Questions, Answers
from app.users.models import UserQuestionAttempts


class QuizService:
    @classmethod
    async def add_quiz(cls, question, answers, true_id, type_="quiz"):
        async with async_session_maker() as session:
            question = Questions(text=question, type=type_)
            for i in range(len(answers)):
                answer = Answers(text=answers[i], is_true=(i == true_id))
                question.answers.append(answer)

            session.add(question)
            await session.commit()
            await session.refresh(question)

            return question

    @classmethod
    async def delete_question(cls, question_id):
        async with async_session_maker() as session:
            stmt = delete(Answers).filter_by(question_id=question_id)
            await session.execute(stmt)

            stmt = delete(UserQuestionAttempts).filter_by(question_id=question_id)
            await session.execute(stmt)

            stmt = delete(lesson_question_association).filter_by(question_id=question_id)
            await session.execute(stmt)

            stmt = delete(Questions).filter_by(id=question_id)
            await session.execute(stmt)

            await session.commit()


    @classmethod
    async def get_question(cls, **filters) -> Questions:
        async with async_session_maker() as session:
            stmt = select(Questions).filter_by(**filters).options(
                selectinload(Questions.answers))
            result = await session.execute(stmt)

            return result.scalars().one()


            # stmt = select(Questions).order_by(func.random()).options(
            #     selectinload(Questions.answers))

            # result = await session.execute(stmt)
            # question = result.scalars().one()
            # options = []
            # shuffle(question.answers)
            # correct_option_id = 0
            # for i in range(len(question.answers)):
            #     options.append(question.answers[i].text)
            #     if question.answers[i].is_true:
            #         correct_option_id = i
            # return {
            #     'question': question.text,
            #     'options': options,
            #     'type': 'quiz',
            #     'open_period': 60,
            #     'correct_option_id': correct_option_id,
            #     'protect_content': True,
            #     'is_anonymous': True
            # }

