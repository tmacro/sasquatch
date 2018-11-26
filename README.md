
# Sasquatch

A mini-language for specifying complex s3 API operations in a concise manner.

```
    # List objects in "mybucket"
    # Filter object keys matching regex ".*\.mp4"
    # Copy matching objects to "mymp4s"
    > sq 'ls:mymedia | gr:.*\.mp4$ | cp:mymp4s'
      Copying mymedia/hello_world.mp4....Done
      Copying mymedia/sasquatch_sighting!.mp4....

```
