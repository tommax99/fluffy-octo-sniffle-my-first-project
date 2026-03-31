from pydantic import BaseModel, EmailStr, UUID4, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    PROJECT_MANAGER = "project_manager"
    MEMBER = "member"


class TaskStatusEnum(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"


class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# Token schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None


class RefreshToken(BaseModel):
    refresh_token: str


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    id: UUID4
    role: UserRoleEnum
    is_active: bool
    is_admin: bool
    avatar_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Workspace schemas
class WorkspaceBase(BaseModel):
    name: str
    description: Optional[str] = None


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class WorkspaceResponse(WorkspaceBase):
    id: UUID4
    owner_id: UUID4
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WorkspaceMemberResponse(BaseModel):
    id: UUID4
    workspace_id: UUID4
    user_id: UUID4
    role: UserRoleEnum
    joined_at: datetime
    user: UserResponse
    
    class Config:
        from_attributes = True


# Project schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None


class ProjectCreate(ProjectBase):
    workspace_id: UUID4


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    is_archived: Optional[bool] = None


class ProjectResponse(ProjectBase):
    id: UUID4
    workspace_id: UUID4
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Column schemas
class ColumnBase(BaseModel):
    name: str
    position: int
    color: Optional[str] = None


class ColumnCreate(ColumnBase):
    project_id: UUID4


class ColumnUpdate(BaseModel):
    name: Optional[str] = None
    position: Optional[int] = None
    color: Optional[str] = None


class ColumnResponse(ColumnBase):
    id: UUID4
    project_id: UUID4
    created_at: datetime
    
    class Config:
        from_attributes = True


# Label schemas
class LabelBase(BaseModel):
    name: str
    color: str


class LabelCreate(LabelBase):
    project_id: UUID4


class LabelUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None


class LabelResponse(LabelBase):
    id: UUID4
    project_id: UUID4
    created_at: datetime
    
    class Config:
        from_attributes = True


# Subtask schemas
class SubtaskBase(BaseModel):
    title: str
    position: int


class SubtaskCreate(SubtaskBase):
    parent_task_id: UUID4


class SubtaskUpdate(BaseModel):
    title: Optional[str] = None
    is_completed: Optional[bool] = None
    position: Optional[int] = None


class SubtaskResponse(SubtaskBase):
    id: UUID4
    parent_task_id: UUID4
    is_completed: bool
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Comment schemas
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    task_id: UUID4
    parent_comment_id: Optional[UUID4] = None


class CommentUpdate(BaseModel):
    content: Optional[str] = None


class CommentResponse(CommentBase):
    id: UUID4
    task_id: UUID4
    author_id: UUID4
    parent_comment_id: Optional[UUID4] = None
    created_at: datetime
    updated_at: datetime
    author: UserResponse
    replies: Optional[List["CommentResponse"]] = None
    
    class Config:
        from_attributes = True


# Attachment schemas
class AttachmentBase(BaseModel):
    filename: str
    file_path: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None


class AttachmentCreate(AttachmentBase):
    task_id: UUID4
    uploaded_by_id: UUID4


class AttachmentResponse(AttachmentBase):
    id: UUID4
    task_id: UUID4
    uploaded_by_id: UUID4
    created_at: datetime
    
    class Config:
        from_attributes = True


# Task schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: PriorityEnum = PriorityEnum.MEDIUM
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    project_id: UUID4
    column_id: UUID4
    assignee_id: Optional[UUID4] = None
    position: int


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    column_id: Optional[UUID4] = None
    assignee_id: Optional[UUID4] = None
    status: Optional[TaskStatusEnum] = None
    priority: Optional[PriorityEnum] = None
    position: Optional[int] = None
    due_date: Optional[datetime] = None


class TaskResponse(TaskBase):
    id: UUID4
    project_id: UUID4
    column_id: Optional[UUID4]
    creator_id: UUID4
    assignee_id: Optional[UUID4] = None
    status: TaskStatusEnum
    priority: PriorityEnum
    position: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    assignee: Optional[UserResponse] = None
    creator: Optional[UserResponse] = None
    column: Optional[ColumnResponse] = None
    subtasks: Optional[List[SubtaskResponse]] = None
    comments: Optional[List[CommentResponse]] = None
    labels: Optional[List[LabelResponse]] = None
    
    class Config:
        from_attributes = True


# Activity Log schemas
class ActivityLogBase(BaseModel):
    action: str
    entity_type: Optional[str] = None
    entity_id: Optional[UUID4] = None
    old_value: Optional[dict] = None
    new_value: Optional[dict] = None


class ActivityLogCreate(ActivityLogBase):
    user_id: UUID4
    task_id: Optional[UUID4] = None


class ActivityLogResponse(ActivityLogBase):
    id: UUID4
    user_id: UUID4
    task_id: Optional[UUID4] = None
    created_at: datetime
    user: UserResponse
    
    class Config:
        from_attributes = True
