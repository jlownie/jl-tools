# Minimum and maximum wait times (in seconds) for trigger
$minwait=2
$maxwait=7

# Length of time (in milliseconds) that the shot window stays open - the conclusion sound plays after this interval
$window=1500

# Length of time (in seconds) between rounds
$reset=5 

do {
    # Start round
    (New-Object Media.SoundPlayer "C:\WINDOWS\Media\chimes.wav").Play();

    # Wait a random period
    $wait=Get-Random -Minimum $minwait -Maximum $maxwait
    Start-Sleep -Seconds $wait
    
    # Play the trigger sound
    (New-Object Media.SoundPlayer "C:\WINDOWS\Media\Windows Ding.wav").Play();
    
    # Wait a set period
    Start-Sleep -Milliseconds $window
    
    # Play the conclusion sound
    (New-Object Media.SoundPlayer "C:\WINDOWS\Media\notify.wav").Play();
    
    # Wait the reset time
    Start-Sleep -Seconds $reset
}
while( $true)