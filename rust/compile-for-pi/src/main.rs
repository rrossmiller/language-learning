use librespot::core::cache::Cache;
use rand::seq::SliceRandom;
use std::path;

use std::env;

use librespot::core::authentication::Credentials;
use librespot::core::config::SessionConfig;
use librespot::core::session::Session;
use librespot::core::spotify_id::SpotifyId;
use librespot::metadata::{Metadata, Playlist, Track};
use librespot::playback::audio_backend;
use librespot::playback::config::{AudioFormat, PlayerConfig};
use librespot::playback::mixer::NoOpVolume;
use librespot::playback::player::Player;

const CREDS_PATH: &str = "creds";
const VOL_PATH: &str = "vol";
const AUDIO_PATH: &str = "audio";
const CACHE_PATH: &str = ".spotify_cache";

pub fn get_home_path() -> Result<path::PathBuf, ()> {
    let mut home_path: path::PathBuf;
    if let Some(pth) = home::home_dir() {
        home_path = pth;
    } else {
        return Err(());
    }

    home_path.push(CACHE_PATH);
    Ok(home_path)
}
pub async fn play_alarm() {
    let home_path = get_home_path().expect("Unable to get your home directory");
    let cache = Cache::new(
        Some(format!("{}/{}", home_path.to_str().unwrap(), CREDS_PATH)),
        Some(format!("{}/{}", home_path.to_str().unwrap(), VOL_PATH)),
        Some(format!("{}/{}", home_path.to_str().unwrap(), AUDIO_PATH)),
        None,
    )
    .unwrap();

    let credentials = match cache.credentials() {
        Some(c) => {
            println!("using saved credentials");
            c
        }
        None => {
            let args: Vec<_> = env::args().collect();
            if args.len() != 3 {
                eprintln!("Usage: {} USERNAME PASSWORD", args[0]);
                return;
            }
            let cred = Credentials::with_password(&args[1], &args[2]);

            cache.save_credentials(&cred);
            cred
        }
    };

    let mut rng = rand::thread_rng();
    let session_config = SessionConfig::default();
    let player_config = PlayerConfig::default();
    let audio_format = AudioFormat::default();
    let backend = audio_backend::find(None).unwrap();

    println!("Connecting ..");
    let (session, _) = Session::connect(session_config, credentials, None, false)
        .await
        .unwrap();

    let (mut player, _) = Player::new(
        player_config,
        session.clone(),
        Box::new(NoOpVolume),
        move || backend(None, audio_format),
    );

    println!("Playing...");
    loop {
        // pick a random track from the alarm playlist
        let plist = "spotify:playlist:2aBMj4vGrpxavecIWQtcc4"; // alarm
                                                               // let plist = "spotify:playlist:4Sxwf25ZF9QaySClmygJEb"; // st party
        let plist_uri = SpotifyId::from_uri(plist).unwrap();

        let plist = Playlist::get(&session, plist_uri).await.unwrap();
        let track = *plist.tracks.choose(&mut rng).unwrap();
        let print_track = Track::get(&session, track).await.unwrap();
        println!("{}", print_track.name);

        // play the track

        player.load(track, true, 0);
        player.await_end_of_track().await;
    }
}

#[tokio::main]
async fn main() {
    play_alarm().await;
}
