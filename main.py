from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from profiles import models
from profiles.db import engine
from profiles.routers import profile, user, singin, verify, node, edge, tree, nodeinfo, human

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

app.include_router(singin.router)
app.include_router(verify.router)
app.include_router(profile.router)
app.include_router(user.router)
app.include_router(node.router)
app.include_router(edge.router)
app.include_router(tree.router)
app.include_router(nodeinfo.router)
app.include_router(human.router)


