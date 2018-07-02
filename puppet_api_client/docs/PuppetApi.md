# swagger_client.PuppetApi

All URIs are relative to *https://localhost:50002/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_puppet**](PuppetApi.md#create_puppet) | **POST** /puppet | Create new Puppet model
[**draw**](PuppetApi.md#draw) | **POST** /puppet/{puppetId}/draw | Draw new image based on the Puppet and input pose
[**estimate_pose**](PuppetApi.md#estimate_pose) | **POST** /puppet/{puppetId}/estimate_pose | Estimate the pose from input image


# **create_puppet**
> Puppet create_puppet(puppet_image)

Create new Puppet model

Before render an image, you should upload a source image as a Puppet template

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PuppetApi()
puppet_image = '/path/to/file.txt' # file | The source image file, JPEG or PNG.

try:
    # Create new Puppet model
    api_response = api_instance.create_puppet(puppet_image)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PuppetApi->create_puppet: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **puppet_image** | **file**| The source image file, JPEG or PNG. | 

### Return type

[**Puppet**](Puppet.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **draw**
> file draw(puppet_id, pose)

Draw new image based on the Puppet and input pose

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PuppetApi()
puppet_id = 'puppet_id_example' # str | ID of the Puppet
pose = swagger_client.Pose() # Pose | 

try:
    # Draw new image based on the Puppet and input pose
    api_response = api_instance.draw(puppet_id, pose)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PuppetApi->draw: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **puppet_id** | **str**| ID of the Puppet | 
 **pose** | [**Pose**](Pose.md)|  | 

### Return type

[**file**](file.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: image/png

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **estimate_pose**
> Crowd estimate_pose(puppet_id, pose_image)

Estimate the pose from input image

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PuppetApi()
puppet_id = 'puppet_id_example' # str | ID of the Puppet
pose_image = '/path/to/file.txt' # file | The target pose image file, JPEG or PNG.

try:
    # Estimate the pose from input image
    api_response = api_instance.estimate_pose(puppet_id, pose_image)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PuppetApi->estimate_pose: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **puppet_id** | **str**| ID of the Puppet | 
 **pose_image** | **file**| The target pose image file, JPEG or PNG. | 

### Return type

[**Crowd**](Crowd.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

