"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from navbar.views import NavbarListView
from awaiting_projects.views import AwaitingProjectsListView, awaitingProjectsAPIDescription,AwaitingProjectRetriveUpdateView,awaitingProjectApproveView,awaitingProjectRejectView,awaitingProjectSnoozeView
from rejectedProject.views import RejectedProjectRetriveUpdateView, RejectedReasonSelectView,rejectedProjectApproveView

from project.views import ProjectListView,projectsAPIDescription
from morning_api.views import morningWebhookClientView,morningWebhookDocumentView


from morning_api.api import test
from project.views import ProjectRetriveUpdateView,get_project_accounting_docs
from rejectedProject.views import RejectedProjectListView,rejectedProjectsAPIDescription
from accounting.views import AccountingDocListView,accountingDocsAPIDescription,get_accounting_docs_morning_info,create_invoice_from_price_proposals,create_cancel_invoice_from_invoice
from accounting.views import get_related_accouting_docs
from positiveCashFlow.views import PositiveCashFlowInvoiceView,PositiveCashFlowProjectView
from done_projects.views import DoneProjectListView,doneProjectsAPIDescription
urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('admin/', admin.site.urls),
    path('navbar/', NavbarListView.as_view()),
    
    # awaiting-projects
    path('awaiting-projects/', AwaitingProjectsListView.as_view()),
    path('awaiting-projects-description/',awaitingProjectsAPIDescription),
    
    path('awaiting-projects/<int:pk>/', AwaitingProjectRetriveUpdateView.as_view()),
    path('awaiting-projects/<int:pk>/approve/', awaitingProjectApproveView),
    path('awaiting-projects/<int:pk>/reject/', awaitingProjectRejectView),
    path('awaiting-projects/<int:pk>/snooze/', awaitingProjectSnoozeView),
    
    path('reject-reasons/', RejectedReasonSelectView.as_view()),
    
    
    # projects
    path('projects/', ProjectListView.as_view()),
    path('projects-description/', projectsAPIDescription),
    
    # done projects
    path('done-projects/', DoneProjectListView.as_view()),
    path('done-projects-description/', doneProjectsAPIDescription),
    
    path('projects/<int:pk>/', ProjectRetriveUpdateView.as_view()),
    path('projects/<int:pk>/accounting-docs/', get_project_accounting_docs),
    
    
    # rejected-projects
    path('rejected-projects/', RejectedProjectListView.as_view()),
    path('rejected-projects-description/', rejectedProjectsAPIDescription),
    path('rejected-projects/<int:pk>/', RejectedProjectRetriveUpdateView.as_view()),
    path('rejected-projects/<int:pk>/approve/', rejectedProjectApproveView),
    
    # accounting
    path('accounting-docs/', AccountingDocListView.as_view()),
    path('accounting-docs-description/', accountingDocsAPIDescription),
    
    path('accounting-docs/<int:pk>/related-docs/', get_related_accouting_docs),
    
    path('accounting-docs-morning-info/', get_accounting_docs_morning_info), # used to create invoice from price proposals
    
    path('create-invoice/', create_invoice_from_price_proposals),
    path('create-cancel-invoice/', create_cancel_invoice_from_invoice),
    
    # possitive cash flow
    path('positive-cash-flow-invoice/',PositiveCashFlowInvoiceView.as_view()),
    path('positive-cash-flow-project/',PositiveCashFlowProjectView.as_view()),
    
    
    # morning-webhook
    
    path('morning-webkook/client/', morningWebhookClientView),
    path('morning-webkook/document/', morningWebhookDocumentView),
    
    
    path('test/', test)
]
