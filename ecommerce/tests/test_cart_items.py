import pytest 

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND
)


# ! Test For Anynomous User
class TestCartItemForAnynomousUser:
    
    def test_if_user_is_anynomous_for_get_method_return_401(
            self,
            get_method_fixture #Fixture
        ):
        """
        Test Method for returning 401 unauthorized status when 
        a anynomous user tries to GET cart endpoint
        """

        # ! Fixture for get method is called
        response=get_method_fixture("/api/e-commerce/cart/1/items/")

        assert response.status_code==HTTP_401_UNAUTHORIZED

# ! Test For Cart For Normal User 
@pytest.mark.django_db
class TestCartItemForNormalUser:
    
    # def test_if_user_is_normal_user_for_get_method_return_200(
    #         self,
    #         get_method_fixture, #Fixture
    #         normal_user_authenticate_fixture #Fixture

    #     ):
    #     """
    #     Test Method for returning 200 OK status when 
    #     normal user perform GET method in cart endpoint
    #     """

    #     # ! Authenticating user as normal user 
    #     normal_user_authenticate_fixture()

    #     # ! Fixture for get method is called
    #     response=get_method_fixture("/api/e-commerce/cart/5/items/")

    #     assert response.status_code==HTTP_200_OK
    

    def test_if_user_is_normal_user_for_delete_method_return_404(
            self,
            delete_method_fixture, #Fixture
            normal_user_authenticate_fixture #Fixture

        ):
        """
        Test Method for returning 404 Not FoundS status when 
        normal user perform GET method in cart endpoint
        """

        # ! Authenticating user as normal user 
        normal_user_authenticate_fixture()

        # ! Fixture for get method is called
        response=delete_method_fixture("/api/e-commerce/cart/5/items/",99)

        assert response.status_code==HTTP_404_NOT_FOUND


# ! Test For Cart For Admin User 
# @pytest.mark.django_db
# class TestCartItemForAdminUser:
        
#     def test_if_user_is_admin_user_for_get_method_return_200(
#             self,
#             get_method_fixture, #Fixture
#             admin_user_authenticate_fixture #Fixture

#         ):
#         """
#         Test Method for returning 200 OK status when 
#         admin user perform GET method in cart endpoint
#         """

#         # ! Authenticating user as admin user 
#         admin_user_authenticate_fixture()

#         # ! Fixture for get method is called
#         response=get_method_fixture("/api/e-commerce/cart/3/items/")

#         assert response.status_code==HTTP_200_OK


    



    

        


        
        
    