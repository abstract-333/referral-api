from typing import Any
from fastapi import APIRouter
from admin import (
    UserAdmin,
    StudentAdmin,
    SpecialityAdmin,
    StudyPeriodsAdmin,
    LecturerAdmin,
    SupervisorsAdmin,
    TokenBlacklistAdmin,
    CourseAdmin,
    TaughtCourseAdmin,
    FacultyAdmin,
    CourseLecturerAdmin,
    SpecialityCourseAdmin,
)
from api import (
    auth_router,
    user_router,
    student_router,
    faculty_router,
    lecturer_router,
    speciality_router,
    health_router,
    file_router,
)

routers: list[APIRouter] = [
    file_router,
    health_router,
    auth_router,
    user_router,
    student_router,
    lecturer_router,
    faculty_router,
    speciality_router,
]
views: list[Any] = [
    UserAdmin,
    StudentAdmin,
    LecturerAdmin,
    SupervisorsAdmin,
    CourseAdmin,
    TaughtCourseAdmin,
    CourseLecturerAdmin,
    SpecialityCourseAdmin,
    FacultyAdmin,
    StudyPeriodsAdmin,
    SpecialityAdmin,
    TokenBlacklistAdmin,
]
