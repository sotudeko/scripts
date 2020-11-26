#include <boost/uuid/uuid_generators.hpp>

int main() {
  const auto uuid = boost::uuids::random_generator();
}