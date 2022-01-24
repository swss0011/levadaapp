from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from profiles import models
from profiles.db import engine
from profiles.routers import profile, user, singin, verify, node, edge, tree, nodeinfo, rw_for_tree, tree_guest, person, from_mother_to_son #,human
#test comment
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
app.include_router(tree_guest.router)
app.include_router(tree.router)
app.include_router(rw_for_tree.router)
app.include_router(nodeinfo.router)
app.include_router(person.router)
app.include_router(from_mother_to_son.router)
#app.include_router(human.router)


