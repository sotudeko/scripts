#include <boost/uuid/uuid_generators.hpp>
#include <MyLib.h>
#include <iostream>



int main() {
  MyLib a;
  a.doNothing();
  const auto uuid = boost::uuids::random_generator();
  std::cout << "Hello from doNothing" << std::endl;

}

