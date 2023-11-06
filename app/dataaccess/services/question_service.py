from app.dataaccess.models import Lessons
from app.dataaccess.models import Questions
from app.dataaccess.utils.unitofwork import SqlAlchemyUnitOfWork


async def add_questions_to_lesson(questions: list[Questions], lesson: Lessons):
    uow = SqlAlchemyUnitOfWork()
    async with uow:
        for question in questions:
            lesson.questions.append(question)

        await uow.add(lesson)
        await uow.commit()


async def add_quiz(question_text, answers, true_id, type_="quiz"):
    uow = SqlAlchemyUnitOfWork()
    async with uow:
        question = await uow.questions.add_one(text=question_text, type=type_)
        for i in range(len(answers)):
            answer = await uow.answers.add_one(text=answers[i],
                                               is_true=(i == true_id))
            await question.answers.append(answer)

        await uow.add(question)
        await uow.commit()
        await uow.refresh(question)

        return question


async def add_questions_for_user(user_id: int, questions: list[int]):
    uow = SqlAlchemyUnitOfWork()
    async with uow:
        for question_id in questions:
            await uow.user_attempts.add_one(user_id=user_id,
                                            question_id=question_id)
        await uow.commit()


async def delete_question(question_id):
    uow = SqlAlchemyUnitOfWork()
    async with uow:
        await uow.answers.delete_all(question_id=question_id)
        await uow.user_attempts.delete_all(question_id=question_id)
        await uow.lessons.delete_question(question_id=question_id)
        await uow.questions.delete_one(id_=question_id)
        await uow.commit()
