from django.urls import path
from diagrams.views import RetrieveAllDiagramsView, RetrieveOneDiagramView

urlpatterns = [
    path('retrieve-diagrams/', RetrieveAllDiagramsView.as_view(), name='retrieve_all_diagrams'),
    path('retrieve-one-diagram/', RetrieveOneDiagramView.as_view(), name='retrieve_one_diagram')
]
