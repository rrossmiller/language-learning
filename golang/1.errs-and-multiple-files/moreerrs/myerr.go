package moreerrs

type MyErr struct{}
func (e *MyErr) Error() string{
	return "you made an Err!"
}