IMAGE_NAME="trc2025_img:1.1.0"
CONTAINER_NAME="trc2025_cont_11"

# ENVIRONMENT += -e "GZ_SIM_RESOURCE_PATH="/root/ros_ws/src/multidrones_ws/multidrones_test/models/gazebo/""
# Define the folder where all sub-Makefiles are stored
SUB_MAKEFILES_DIR := sub_makefiles

# Default option if none is provided
DEFAULT_OPTION := linux

# Use the 'option' variable if provided, otherwise default to DEFAULT_OPTION
OPTION ?= $(DEFAULT_OPTION)

# Dynamically include the corresponding Makefile if it exists
ifneq ("$(wildcard $(SUB_MAKEFILES_DIR)/$(OPTION).mk)","")
    include $(SUB_MAKEFILES_DIR)/$(OPTION).mk
else
    $(error Makefile for option '$(OPTION)' not found in $(SUB_MAKEFILES_DIR))
endif


## Manage source code
SRC_DIR = ./src

create_src:
	mkdir -p ./src/ros_ws/src/trc2025
	cp -r ../crazyflie_lcis $(SRC_DIR)/ros_ws/src/trc2025/
	cp -r ../crazyflie_lcis_bringup $(SRC_DIR)/ros_ws/src/trc2025/
	cp -r ../crazyflie_lcis_description $(SRC_DIR)/ros_ws/src/trc2025/
	cp -r ../crazyflie_lcis_examples $(SRC_DIR)/ros_ws/src/trc2025/
	cp -r ../crazyflie_lcis_gazebo $(SRC_DIR)/ros_ws/src/trc2025/


sync_src:
	docker cp $(CONTAINER_NAME):/root/ros_ws/src/. $(SRC_DIR)/ros_ws/src

#	docker cp $(CONTAINER_NAME):/root/crazyflie-lib-python/. $(SRC_DIR)/crazyflie-lib-python
#	docker cp $(CONTAINER_NAME):/root/crazyflie-firmware/. $(SRC_DIR)/crazyflie-firmware

update_con_src:
	docker cp $(SRC_DIR)/ros_ws/src/. $(CONTAINER_NAME):/root/ros_ws/src




######################################################

build_img:
	docker build -t $(IMAGE_NAME) -f ./Dockerfile ..


##### Docker container #####	
# create docker container
create_con: build_img
ifeq ($(filter linux linux_nogpu, $(OPTION)),)
	@docker run -it \
	--rm \
	--name $(CONTAINER_NAME) \
	$(ENVIRONMENT) \
	$(DEV) \
	$(NET) \
	$(GPU) \
	$(VOLUME) \
	$(IMAGE_NAME) \
	bash
else
	xhost +local:root
	@docker run -it \
	--rm \
	--name $(CONTAINER_NAME) \
	$(ENVIRONMENT) \
	$(DEV) \
	$(NET) \
	$(GPU) \
	$(VOLUME) \
	$(IMAGE_NAME) \
	bash
	
	xhost -local:root
endif

access_con:
	docker exec -it $(CONTAINER_NAME) bash 


##### Clean images/containers #####
# remove docker image
clean_img: 
	# IMAGE_ID=$(cat logs/image_id.txt) 
	# @docker rmi -f $(IMAGE_ID)
	docker rmi -f $(IMAGE_NAME)
	
clean_con: 
	@docker stop $(CONTAINER_NAME)
	@docker rm $(CONTAINER_NAME)