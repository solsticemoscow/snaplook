# import datetime
#
# from sqlalchemy import String, func
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from .base import DBModel
#
#
# class Clinic(DBModel):
#     """Clinic - """
#     __tablename__ = 'clinics'
#
#     id: Mapped[str] = mapped_column(String(200), primary_key=True, index=True, unique=True)
#
#     name: Mapped[str] = mapped_column(String(200), nullable=False)
#     is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
#     created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), nullable=False)
#
#     clinics_to_devices = relationship('Device', back_populates='devices_to_clinics')
#     clinics_to_task = relationship("Task", back_populates="task_to_clinics")
