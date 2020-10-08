package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
)

func main() {
	var files []string

	// music_lib := "/Volumes/Users/sola/Music/iTunes/iTunes Music"
	music_lib := "/Users/sotudeko/Downloads"

	err := filepath.Walk(music_lib, visit(&files))

	if err != nil {
		panic(err)
	}

	for _, file := range files {
		fmt.Println(file)
	}
}

func visit(files *[]string) filepath.WalkFunc {
    return func(path string, info os.FileInfo, err error) error {

        if err != nil {
            log.Fatal(err)
		}
		
		if info.IsDir() {
			*files = append(*files, path)
		}

        return nil
    }
}





