cmake_minimum_required(VERSION 3.8)
project(crazyflie_lcis_gazebo)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

find_package(gz-cmake3 REQUIRED)
find_package(gz-plugin2 REQUIRED COMPONENTS register)
set(GZ_PLUGIN_VER ${gz-plugin2_VERSION_MAJOR})
find_package(gz-common5 REQUIRED COMPONENTS profiler)
set(GZ_COMMON_VER ${gz-common5_VERSION_MAJOR})


set(GZ_SIM_FOUND FALSE)
foreach(ver 8 7) # replace with future gz-sim versions
  if(NOT GZ_SIM_FOUND)
    find_package(gz-sim NAMES gz-sim${ver})
    if(gz-sim_FOUND)
      set(GZ_SIM_VER ${gz-sim_VERSION_MAJOR})
      set(GZ_SIM_FOUND TRUE)
    endif()
  endif()
endforeach()

if(NOT GZ_SIM_FOUND)
  message(FATAL_ERROR "gz-sim not found")
endif()

if(GZ_SIM_VER EQUAL 8)
  message("Found Gazebo 8: Harmonic")
  find_package(gz-transport REQUIRED NAMES gz-transport13)
  find_package(gz-msgs REQUIRED NAMES gz-msgs10)
elseif(GZ_SIM_VER EQUAL 7)
  message("Found Gazebo 7: Garden")
  find_package(gz-transport REQUIRED NAMES gz-transport12)
  find_package(gz-msgs REQUIRED NAMES gz-msgs9)
endif()

set(GZ_TRANSPORT_VER ${gz-transport_VERSION_MAJOR})
set(GZ_MSGS_VER ${gz-msgs_VERSION_MAJOR})

#======================================= CrazySim PLUGIN ==========================================//
# Following 'add_library' directive defines a library target named 'crazysim_plugin'.
# The 'SHARED' keyword indicates that a shared library should be compiled, and
# is followed by the list of source files for the target.
add_library(gz_crazysim_plugin
  SHARED
  src/crazysim_plugin.cpp
)

# Following 'target_include_directories' directive specifies 'include' as the
# include directory to use when compiling the 'crazysim_plugin' target.
# The 'PRIVATE' keyword specifies that this directive will populate the
# INCLUDE_DIRECTORIES property for the 'crazysim_plugin' target.
target_include_directories(
  gz_crazysim_plugin PRIVATE include/${PROJECT_NAME}
)


#==================== Additional ======================#
set_property(TARGET gz_crazysim_plugin PROPERTY CXX_STANDARD 20)


# Following 'target_link_libraries' directive specifies to use the 
# gz-sim library when linking the 'crazysim_plugin' target.
# The 'PRIVATE' keyword stipulates that the gz-sim library will not
# automatically be included if the 'crazysim_plugin' target were to
# be linked to anoter target. 
# ${GZ_SIM_VER} is substituted by the value that is was set to above.
target_link_libraries(gz_crazysim_plugin 
  PRIVATE
    gz-plugin${GZ_PLUGIN_VER}::gz-plugin${GZ_PLUGIN_VER}
    gz-sim${GZ_SIM_VER}::gz-sim${GZ_SIM_VER}
    gz-msgs${GZ_MSGS_VER}::gz-msgs${GZ_MSGS_VER}
    gz-transport${GZ_TRANSPORT_VER}::core
)


# Following 'install' directive ensures that the compiled libraries
# of the 'BasicSystem' and 'FullSystem' targets will be copied
# to the subfolder 'lib/ros_gz_example_gazebo' of the install directory.
install(
  TARGETS gz_crazysim_plugin
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()


# Following hooks are used to ensure that the correct environment variables
# will be set by exectuting 'source install/setup.bash' after compilation.
# When using this template for your project, change the filenames of the
# files in the 'hooks' folder, to correspond to your project name.
ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/${PROJECT_NAME}.dsv.in")
ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/${PROJECT_NAME}.sh.in")


ament_package()
