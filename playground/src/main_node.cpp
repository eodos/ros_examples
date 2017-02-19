#include <ros/ros.h>

#include <std_msgs/String.h>
#include <sstream>

#include <tf/transform_broadcaster.h>
#include <turtlesim/Pose.h>

std::string turtle_name;

void poseCallback(const turtlesim::PoseConstPtr& msg)
{
	static tf::TransformBroadcaster br;
	tf::Transform transform;
	transform.setOrigin(tf::Vector3(msg->x, msg->y, 0.0));
	tf::Quaternion q;
	q.setRPY(0, 0, msg->theta);
	transform.setRotation(q);
	br.sendTransform(tf::StampedTransform(transform, ros::Time::now(), "world", turtle_name));
}

int main(int argc, char **argv)
{
	ros::init(argc, argv, "main_node");
	ros::NodeHandle n;

	if (argc != 2)
	{
		ROS_ERROR("need turtle name as argument");
		return -1;
	}

	turtle_name = argv[1];

	ros::Subscriber sub = n.subscribe(turtle_name+"/pose", 10, &poseCallback);

	ros::Publisher pub = n.advertise<std_msgs::String>("test_topic", 1000);
	ros::Rate loop_rate(2);

	while (ros::ok())
	{
		std_msgs::String msg;
		std::stringstream ss;
		ss << "hello world";
		msg.data = ss.str();

		ROS_INFO("%s", msg.data.c_str());

		// pub.publish(msg);
		// ros::spinOnce();
		// loop_rate.sleep();
		ros::spin();
	}

	return 0;
}