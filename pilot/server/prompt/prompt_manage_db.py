from datetime import datetime

from sqlalchemy import Column, Integer, Text, String, DateTime

from pilot.base_modules.meta_data.base_dao import BaseDao
from pilot.base_modules.meta_data.meta_data import Base, engine, session
from pilot.configs.config import Config

from pilot.server.prompt.request.request import PromptManageRequest

CFG = Config()


class PromptManageEntity(Base):
    __tablename__ = "prompt_manage"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_unicode_ci",
    }
    id = Column(Integer, primary_key=True)
    chat_scene = Column(String(100))
    sub_chat_scene = Column(String(100))
    prompt_type = Column(String(100))
    prompt_name = Column(String(512))
    content = Column(Text)
    user_name = Column(String(128))
    gmt_created = Column(DateTime)
    gmt_modified = Column(DateTime)

    def __repr__(self):
        return f"PromptManageEntity(id={self.id}, chat_scene='{self.chat_scene}', sub_chat_scene='{self.sub_chat_scene}', prompt_type='{self.prompt_type}', prompt_name='{self.prompt_name}', content='{self.content}',user_name='{self.user_name}', gmt_created='{self.gmt_created}', gmt_modified='{self.gmt_modified}')"


class PromptManageDao(BaseDao):
    def __init__(self):
        super().__init__(
            database="dbgpt", orm_base=Base, db_engine=engine, session=session
        )

    def create_prompt(self, prompt: PromptManageRequest):
        session = self.get_session()
        prompt_manage = PromptManageEntity(
            chat_scene=prompt.chat_scene,
            sub_chat_scene=prompt.sub_chat_scene,
            prompt_type=prompt.prompt_type,
            prompt_name=prompt.prompt_name,
            content=prompt.content,
            user_name=prompt.user_name,
            gmt_created=datetime.now(),
            gmt_modified=datetime.now(),
        )
        session.add(prompt_manage)
        session.commit()
        session.close()

    def get_prompts(self, query: PromptManageEntity):
        session = self.get_session()
        prompts = session.query(PromptManageEntity)
        if query.chat_scene is not None:
            prompts = prompts.filter(PromptManageEntity.chat_scene == query.chat_scene)
        if query.sub_chat_scene is not None:
            prompts = prompts.filter(
                PromptManageEntity.sub_chat_scene == query.sub_chat_scene
            )
        if query.prompt_type is not None:
            prompts = prompts.filter(
                PromptManageEntity.prompt_type == query.prompt_type
            )
            if query.prompt_type == "private" and query.user_name is not None:
                prompts = prompts.filter(
                    PromptManageEntity.user_name == query.user_name
                )
        if query.prompt_name is not None:
            prompts = prompts.filter(
                PromptManageEntity.prompt_name == query.prompt_name
            )

        prompts = prompts.order_by(PromptManageEntity.gmt_created.desc())
        result = prompts.all()
        session.close()
        return result

    def update_prompt(self, prompt: PromptManageEntity):
        session = self.get_session()
        session.merge(prompt)
        session.commit()
        session.close()

    def delete_prompt(self, prompt: PromptManageEntity):
        session = self.get_session()
        if prompt:
            session.delete(prompt)
            session.commit()
        session.close()
