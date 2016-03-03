from flask import Flask

app = Flask("huginn")

import huginn.web.views
import huginn.web.api
