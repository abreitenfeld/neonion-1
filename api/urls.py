from django.conf.urls import patterns, url, include
from rest_framework import routers, serializers, viewsets
from accounts.models import User
from documents.models import Document
from neonion.models import Workspace
from annotationsets.models import AnnotationSet, ConceptSource


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'surname', 'joined')


# ViewSets for users.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Serializers define the API representation.
class ConceptSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptSource
        fields = ('linked_concept_uri', 'provider', 'class_name')


# ViewSets for annotation sets.
class ConceptSourceViewSet(viewsets.ModelViewSet):
    queryset = ConceptSource.objects.all()
    serializer_class = ConceptSourceSerializer


# Serializers define the API representation.
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('urn', 'title', 'created', 'updated')


# Serializers define the API representation.
class DetailedDocumentSerializer(DocumentSerializer):
    class Meta:
        model = Document
        fields = ('urn', 'title', 'content', 'created', 'updated')


# ViewSets for document.
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedDocumentSerializer
        else:
            return DocumentSerializer


# Serializers define the API representation.
class AnnotationSetSerializer(serializers.ModelSerializer):
    sources = ConceptSourceSerializer(many=True)

    class Meta:
        model = AnnotationSet
        fields = ('uri', 'label', 'allow_creation', 'sources')


# ViewSets for annotation sets.
class AnnotationSetViewSet(viewsets.ModelViewSet):
    queryset = AnnotationSet.objects.all()
    serializer_class = AnnotationSetSerializer


# Serializers define the API representation.
class WorkspaceSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer()
    documents = DocumentSerializer(many=True)
    annotation_sets = AnnotationSetSerializer(many=True)

    class Meta:
        model = Workspace
        fields = ('owner', 'documents', 'annotation_sets')


# ViewSets for document.
class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'workspaces', WorkspaceViewSet)
router.register(r'annotationsets', AnnotationSetViewSet)
router.register(r'conceptsources', ConceptSourceViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^workspace/$', 'api.views.personal_workspace'),
)