from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from uuid import UUID

from app.models import Task, TaskStatus, Priority, Column
from app.schemas import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, task_id: UUID) -> Optional[Task]:
        result = await self.db.execute(
            select(Task)
            .where(Task.id == task_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_project(self, project_id: UUID, skip: int = 0, limit: int = 100) -> List[Task]:
        result = await self.db.execute(
            select(Task)
            .where(Task.project_id == project_id)
            .order_by(Task.position)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_column(self, column_id: UUID) -> List[Task]:
        result = await self.db.execute(
            select(Task)
            .where(Task.column_id == column_id)
            .order_by(Task.position)
        )
        return list(result.scalars().all())
    
    async def get_by_assignee(self, assignee_id: UUID, skip: int = 0, limit: int = 100) -> List[Task]:
        result = await self.db.execute(
            select(Task)
            .where(Task.assignee_id == assignee_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, task_data: TaskCreate) -> Task:
        task = Task(**task_data.model_dump())
        self.db.add(task)
        await self.db.flush()
        await self.db.refresh(task)
        return task
    
    async def update(self, task: Task, update_data: TaskUpdate) -> Task:
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(task, field, value)
        
        # Auto-update status based on column or completion
        if update_dict.get("column_id") or "column_id" in update_dict:
            # Could auto-update status based on column
            pass
        
        if task.status == TaskStatus.DONE and not task.completed_at:
            from datetime import datetime
            task.completed_at = datetime.utcnow()
        elif task.status != TaskStatus.DONE and task.completed_at:
            task.completed_at = None
        
        await self.db.flush()
        await self.db.refresh(task)
        return task
    
    async def delete(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.flush()
    
    async def update_positions(self, column_id: UUID, task_positions: List[tuple[UUID, int]]) -> None:
        """Update positions of multiple tasks in a column"""
        for task_id, position in task_positions:
            result = await self.db.execute(
                select(Task).where(Task.id == task_id)
            )
            task = result.scalar_one_or_none()
            if task and task.column_id == column_id:
                task.position = position
    
    async def move_to_column(self, task: Task, new_column_id: UUID, new_position: int) -> Task:
        old_column_id = task.column_id
        old_position = task.position
        
        task.column_id = new_column_id
        task.position = new_position
        
        await self.db.flush()
        await self.db.refresh(task)
        return task
    
    async def count_by_project(self, project_id: UUID) -> int:
        result = await self.db.execute(
            select(func.count(Task.id)).where(Task.project_id == project_id)
        )
        return result.scalar_one()
    
    async def count_by_status(self, project_id: UUID, status: TaskStatus) -> int:
        result = await self.db.execute(
            select(func.count(Task.id))
            .where(Task.project_id == project_id)
            .where(Task.status == status)
        )
        return result.scalar_one()
    
    async def search(self, project_id: UUID, query: str, skip: int = 0, limit: int = 50) -> List[Task]:
        search_pattern = f"%{query}%"
        result = await self.db.execute(
            select(Task)
            .where(Task.project_id == project_id)
            .where(
                (Task.title.ilike(search_pattern)) |
                (Task.description.ilike(search_pattern))
            )
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
