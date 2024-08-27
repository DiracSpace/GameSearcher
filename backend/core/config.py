#!/usr/bin/env python

from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str
    save_path: str
    cache_path: str

    class Config:
        env_file: str = ".env"
