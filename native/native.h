#include <string>

#ifdef _WIN32
#  define API __declspec(dllexport)
#else
#  define API __attribute__((visibility("default")))
#endif

#ifdef __cplusplus
extern "C" {
#endif

// headers

#ifdef __cplusplus
  }
#endif
