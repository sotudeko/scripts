package main

import (
      "fmt"
      "path/filepath"
      "os"
      "log"
      "syscall"
 
)

func main() {
        err := filepath.Walk(".",
                func(path string, info os.FileInfo, err error) error {
                        if err != nil {
                                return err
                        }

                fileinfo, err := os.Stat(info.Name())
                atime := fileinfo.Sys().(*syscall.Stat_t).Atimespec
                fmt.Println(atime.Sec, path, info.Name())
                //fmt.Println(time.Unix(atime.Sec, atime.Nano()))


                return nil
        })

        if err != nil {
                log.Println(err)
        }
}

