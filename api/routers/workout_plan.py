from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from app.services.auth import AuthService
from app.services.workout_plan import WorkoutPlanService
from app.services.exceptions import NotFoundException
from core.schemas.workout_plan import WorkoutPlanCreate, WorkoutPlanUpdate, WorkoutPlan

WorkoutPlanRouter = APIRouter(
    prefix='/workout-plan', tags=['workout-plan']
    ,dependencies=[Depends(AuthService.get_current_user)]
)

@WorkoutPlanRouter.get("/{workout_plan_id}", response_model=WorkoutPlan)
def get(workout_plan_id: int, workout_plan_service: WorkoutPlanService = Depends()):
    try:
        workout_plan = workout_plan_service.get(workout_plan_id)
        return workout_plan
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Plano de treino não encontrado.")


@WorkoutPlanRouter.get("", response_model=List[WorkoutPlan])
def list(user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 10, workout_plan_service: WorkoutPlanService = Depends()):
    try:
        workout_plan = workout_plan_service.list(user_id, skip, limit)
        return workout_plan
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Nenhum plano de treino associado a esse usuário.")


@WorkoutPlanRouter.post("", response_model=WorkoutPlan)
def create(workout_plan_body: WorkoutPlanCreate, workout_plan_service: WorkoutPlanService = Depends()):
    workout_plan = workout_plan_service.create(workout_plan_body)
    return workout_plan


@WorkoutPlanRouter.put("", response_model=WorkoutPlan)
def update(workout_plan_body: WorkoutPlanUpdate, workout_plan_service: WorkoutPlanService = Depends()):
    try:
        workout_plan = workout_plan_service.update(workout_plan_body)
        return workout_plan
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Exercício não encontrado.")


@WorkoutPlanRouter.delete("/{workout_plan_id}")
def delete(workout_plan_id: int, workout_plan_service: WorkoutPlanService = Depends()):
    try:
        workout_plan_service.delete(workout_plan_id)
        return {"message": "Exercício deletado."}
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Exercício não encontrado.")