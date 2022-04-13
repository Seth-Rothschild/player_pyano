import { useEffect, useState, useRef, useCallback } from "react";

const baseUrl = "http://localhost:3001";

export function App() {

  const [isSending, setIsSending] = useState(false);
  const isMounted = useRef(true)

  // set isMounted to false when we unmount the component
  useEffect(() => {
    return () => {
      isMounted.current = false
    }
  }, [])

    const playSong = useCallback(async () => {
      //don't send again while we are sending
      if (isSending) {
        return;
      } 

      //update state
      setIsSending(true);

      //send actual request
      const url = baseUrl + '/play';
      const res = await fetch(url);

      //once request is sent, update state again
      if (isMounted.current) {
        // only update if we are still mounted
        setIsSending(false);
      }
      const json = await res.json();
    }, [isSending]); //update the callback if the state changes
    
    return (
      <div>
      <button disabled={isSending} onClick={playSong}>
        Play Song
      </button>
    </div>
    );
  }