#!/usr/bin/env python3
import math
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import Empty
from turtlesim.srv import SetPen, TeleportAbsolute


current_pose = None


def pose_callback(msg):
    global current_pose
    current_pose = msg


def normalize_angle(angle):
    """把角度限制在 -pi 到 pi 之间"""
    while angle > math.pi:
        angle -= 2.0 * math.pi
    while angle < -math.pi:
        angle += 2.0 * math.pi
    return angle


def wait_for_pose():
    """等待接收到小海龟位姿信息"""
    rate = rospy.Rate(30)
    while current_pose is None and not rospy.is_shutdown():
        rate.sleep()


def stop(pub):
    """停止小海龟运动，连续发布几次零速度，避免残留速度影响轨迹"""
    vel = Twist()
    rate = rospy.Rate(30)
    for _ in range(10):
        pub.publish(vel)
        rate.sleep()


def rotate_to(pub, target_theta):
    """旋转到指定角度"""
    rate = rospy.Rate(60)

    while not rospy.is_shutdown():
        error = normalize_angle(target_theta - current_pose.theta)

        if abs(error) < 0.005:
            break

        vel = Twist()
        vel.angular.z = 0.8 if error > 0 else -0.8

        pub.publish(vel)
        rate.sleep()

    stop(pub)


def move_forward(pub, distance, target_theta):
    """前进指定距离，并在直线运动过程中持续修正方向"""
    start_x = current_pose.x
    start_y = current_pose.y
    rate = rospy.Rate(60)

    while not rospy.is_shutdown():
        dx = current_pose.x - start_x
        dy = current_pose.y - start_y
        moved = math.sqrt(dx * dx + dy * dy)

        if moved >= distance:
            break

        # 直线运动时持续修正方向，防止中途拐动
        angle_error = normalize_angle(target_theta - current_pose.theta)

        vel = Twist()
        vel.linear.x = 0.6
        vel.angular.z = 1.5 * angle_error

        # 限制纠偏角速度，避免来回抖动
        if vel.angular.z > 0.3:
            vel.angular.z = 0.3
        elif vel.angular.z < -0.3:
            vel.angular.z = -0.3

        pub.publish(vel)
        rate.sleep()

    stop(pub)


def main():
    rospy.init_node("draw_square_node")

    pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
    rospy.Subscriber("/turtle1/pose", Pose, pose_callback)

    rospy.sleep(1)
    wait_for_pose()

    try:
        rospy.wait_for_service("/clear", timeout=3)
        clear = rospy.ServiceProxy("/clear", Empty)

        rospy.wait_for_service("/turtle1/set_pen", timeout=3)
        set_pen = rospy.ServiceProxy("/turtle1/set_pen", SetPen)

        rospy.wait_for_service("/turtle1/teleport_absolute", timeout=3)
        teleport = rospy.ServiceProxy("/turtle1/teleport_absolute", TeleportAbsolute)

        # 清空画布
        clear()

        # 抬笔移动到合适起点，避免画到边界
        set_pen(255, 0, 0, 3, 1)
        teleport(3.0, 3.0, 0.0)

        # 落笔，设置红色轨迹
        set_pen(255, 0, 0, 3, 0)

    except Exception as e:
        rospy.logwarn("Service call failed: %s", e)

    rospy.sleep(1)

    side_length = 3.0

    # 右、上、左、下，四条边
    angles = [
        0.0,
        math.pi / 2,
        math.pi,
        -math.pi / 2
    ]

    for angle in angles:
        rotate_to(pub, angle)
        move_forward(pub, side_length, angle)

    rotate_to(pub, 0.0)
    stop(pub)

    rospy.loginfo("Square drawing finished.")


if __name__ == "__main__":
    main()
