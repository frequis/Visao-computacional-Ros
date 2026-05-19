from setuptools import find_packages, setup

package_name = 'turtle_commander'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('lib/' + package_name, ['scripts/drawer_node']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Seu Nome',
    maintainer_email='seu@email.com',
    description='Pacote Turtle Draw Ponderada',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'drawer_node = turtle_commander.drawer_node:main'
        ],
    },
)