from django.urls import path

from category.views import CategoryListView, CreateCategoryView, DeleteCategoryView, UpdateCategoryView

urlpatterns = [

    path('', CategoryListView.as_view(), name='category_list'),

    path('create/', CreateCategoryView.as_view(), name='create_category'),

    path('update/<int:category_id>', UpdateCategoryView.as_view(), name='update_category'),

    path('delete/<int:category_id>', DeleteCategoryView.as_view(), name='delete_category'),
]
